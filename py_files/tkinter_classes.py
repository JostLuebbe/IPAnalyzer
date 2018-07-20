import logging as lg
import os
import tkinter as tk
import traceback
from datetime import datetime
from tkinter import ttk, scrolledtext, messagebox

import netaddr
import netaddr.core
import xlsxwriter as xw
from PIL import ImageTk, Image


class IPAnalyzerGUI():
    def __init__(self, master):
        self.master = master
        master.title('IPAnalyzer')
        self.master.geometry('1000x500')
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.master.option_add('*tearOff', 'FALSE')
        self.master.report_callback_exception = self.report_callback_exception

        # Declare GUI Variables
        self.left_ip_set = netaddr.IPSet()
        self.right_ip_set = netaddr.IPSet()
        self.intersection_text_variable = tk.StringVar()
        self.left_difference_text_variable = tk.StringVar()
        self.right_difference_text_variable = tk.StringVar()
        self.intersection_set = None
        self.delete_difference_set = None
        self.delete_right_difference_set = None

        # Declare GUI Components
        self.main_frame = tk.Frame(self.master)

        self.left_input_field = scrolledtext.ScrolledText(self.main_frame)
        self.right_input_field = scrolledtext.ScrolledText(self.main_frame)

        self.output_frame = tk.Frame(self.main_frame)

        self.intersection_label = tk.Label(self.output_frame)
        self.intersection_entry_field = tk.Entry(self.output_frame)

        self.left_difference_label = tk.Label(self.output_frame)
        self.left_difference_entry_field = tk.Entry(self.output_frame)

        self.right_difference_label = tk.Label(self.output_frame)
        self.right_difference_entry_field = tk.Entry(self.output_frame)

        self.left_tree = ttk.Treeview(self.main_frame)
        self.right_tree = ttk.Treeview(self.main_frame)

        self.left_tree_vsb = ttk.Scrollbar(self.main_frame)
        self.left_tree_hsb = ttk.Scrollbar(self.main_frame)

        self.right_tree_vsb = ttk.Scrollbar(self.main_frame)
        self.right_tree_hsb = ttk.Scrollbar(self.main_frame)

        self.left_update_button = tk.Button(self.main_frame)
        self.right_update_button = tk.Button(self.main_frame)
        self.export_button = tk.Button(self.output_frame)

        # Customize GUI Components
        self.configure_components()

        # Grid Components
        self.grid_components()

        self.master.lift()

    def configure_components(self):
        tk.Grid.columnconfigure(self.master, 0, weight=1)
        tk.Grid.rowconfigure(self.master, 0, weight=1)

        tk.Grid.columnconfigure(self.main_frame, 0, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 1, weight=0)
        tk.Grid.columnconfigure(self.main_frame, 2, weight=0)
        tk.Grid.columnconfigure(self.main_frame, 3, weight=1)
        tk.Grid.columnconfigure(self.main_frame, 4, weight=0)
        tk.Grid.rowconfigure(self.main_frame, 0, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 1, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 2, weight=0)
        tk.Grid.rowconfigure(self.main_frame, 3, weight=0)

        self.left_tree_vsb.config(
            orient='vertical',
            command=self.left_tree.yview
        )

        self.left_tree_hsb.config(
            orient='horizontal',
            command=self.left_tree.xview
        )

        self.right_tree_vsb.config(
            orient='vertical',
            command=self.right_tree.yview
        )

        self.right_tree_hsb.config(
            orient='horizontal',
            command=self.right_tree.xview
        )

        self.left_tree.config(
            columns=['ips', 'range', 'num'],
            yscrollcommand=self.left_tree_vsb.set,
            xscrollcommand=self.left_tree_hsb.set
        )

        self.left_tree.column('#0', minwidth=50, width=50, stretch=False, anchor=tk.W)
        self.left_tree.column('ips', minwidth=100, width=100, stretch=True, anchor=tk.CENTER)
        self.left_tree.column('range', minwidth=70, width=70, stretch=False, anchor=tk.CENTER)
        self.left_tree.column('num', minwidth=70, width=70, stretch=False, anchor=tk.CENTER)

        self.left_tree.heading('#0', text='')
        self.left_tree.heading('ips', text='IP(s)')
        self.left_tree.heading('range', text='IP Range?')
        self.left_tree.heading('num', text='Num IPs')

        self.left_tree.bind('<Double-1>', lambda event: self.on_double_click_left(event))

        self.right_tree.config(
            columns=['ips', 'range', 'num'],
            yscrollcommand=self.right_tree_vsb.set,
            xscrollcommand=self.right_tree_hsb.set
        )

        self.right_tree.column('#0', minwidth=50, width=50, stretch=False, anchor=tk.W)
        self.right_tree.column('ips', minwidth=100, width=100, stretch=True, anchor=tk.CENTER)
        self.right_tree.column('range', minwidth=70, width=70, stretch=False, anchor=tk.CENTER)
        self.right_tree.column('num', minwidth=70, width=70, stretch=False, anchor=tk.CENTER)

        self.right_tree.heading('#0', text='')
        self.right_tree.heading('ips', text='IP(s)')
        self.right_tree.heading('range', text='IP Range?')
        self.right_tree.heading('num', text='Num IPs')

        self.right_tree.bind('<Double-1>', lambda event: self.on_double_click_right(event))

        self.left_update_button.config(
            text='Update Tree',
            command=self.read_left_input,
            height=2
        )

        self.right_update_button.config(
            text='Update Tree',
            command=self.read_right_input,
            height=2
        )

        self.export_button.config(
            text='Export IPs',
            command=self.export,
            height=2,
            state=tk.DISABLED
        )

        self.intersection_label.config(
            text='Number of IPs in both:',
        )
        self.intersection_entry_field.config(
            textvariable=self.intersection_text_variable,
            state=tk.DISABLED
        )

        self.left_difference_label.config(
            text='Number of IPs only in the left side:',
        )
        self.left_difference_entry_field.config(
            textvariable=self.left_difference_text_variable,
            state=tk.DISABLED
        )

        self.right_difference_label.config(
            text='Number of IPs only in the right side:',
        )
        self.right_difference_entry_field.config(
            textvariable=self.right_difference_text_variable,
            state=tk.DISABLED
        )

    def grid_components(self):
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.left_input_field.grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)
        self.left_tree.grid(column=0, row=1, sticky=tk.NSEW)
        self.left_tree_hsb.grid(column=0, row=2, sticky=tk.EW)
        self.left_update_button.grid(column=0, row=3, columnspan=2, sticky=tk.NSEW)
        self.left_tree_vsb.grid(column=1, row=1, sticky=tk.NS)

        self.right_input_field.grid(column=3, row=0, columnspan=2, sticky=tk.NSEW)
        self.right_tree.grid(column=3, row=1, sticky=tk.NSEW)
        self.right_tree_hsb.grid(column=3, row=2, sticky=tk.EW)
        self.right_update_button.grid(column=3, row=3, columnspan=2, sticky=tk.NSEW)
        self.right_tree_vsb.grid(column=4, row=1, sticky=tk.NS)

        self.output_frame.grid(column=2, row=0, rowspan=4, padx=(50, 50), sticky=tk.NSEW)
        self.intersection_label.grid(column=0, pady=(60, 0), row=0)
        self.intersection_entry_field.grid(column=0, row=1)
        self.left_difference_label.grid(column=0, pady=(60, 0), row=2)
        self.left_difference_entry_field.grid(column=0, row=3)
        self.right_difference_label.grid(column=0, pady=(60, 0), row=4)
        self.right_difference_entry_field.grid(column=0, row=5)
        self.export_button.grid(column=0, row=6)

    @staticmethod
    def call(line):
        try:
            return netaddr.IPNetwork(line)
        except netaddr.core.AddrFormatError as e:
            lg.error(f'Improper formatting of input: {e}')
            return None

    def read_left_input(self):
        if not len(self.left_input_field.get(1.0, tk.END)) - 1:
            tk.messagebox.showwarning('Bad Input', 'Please enter assets to continue with discovery!')
            self.master.lift()
            return

        temp_set = {self.call(line) for line in self.left_input_field.get(1.0, tk.END).splitlines()}
        self.left_ip_set = netaddr.IPSet(x for x in temp_set if x is not None)

        self.left_input_field.delete(1.0, tk.END)

        self.update_left_tree()
        self.update_stats()
        self.export_button['state'] = tk.NORMAL

    def read_right_input(self):
        if not len(self.right_input_field.get(1.0, tk.END)) - 1:
            tk.messagebox.showwarning('Bad Input', 'Please enter assets to continue with discovery!')
            self.master.lift()
            return

        temp_set = {self.call(line) for line in self.right_input_field.get(1.0, tk.END).splitlines()}
        self.right_ip_set = netaddr.IPSet(x for x in temp_set if x is not None)

        self.right_input_field.delete(1.0, tk.END)

        self.update_right_tree()
        self.update_stats()
        self.export_button['state'] = tk.NORMAL

    def update_left_tree(self):
        self.left_tree.delete(*self.left_tree.get_children())

        image = Image.open('resources/images/milker-X-icon.png')
        imwidth = 10
        wpersent = (imwidth / float(image.size[0]))
        hsize = int(float(image.size[1]) * float(wpersent))
        image = ImageTk.PhotoImage(image.resize((imwidth, hsize), Image.ANTIALIAS))

        self.left_tree.image = image

        for item in netaddr.cidr_merge(self.left_ip_set):
            values = list()
            values.append(str(item))

            if '32' in str(item).split('/')[1]:
                values.append(False)
                values.append(1)
            else:
                values.append(True)
                values.append(len(item))

            self.left_tree.insert(
                '',
                tk.END,
                text='',
                image=image,
                values=values
            )

    def update_right_tree(self):
        self.right_tree.delete(*self.right_tree.get_children())

        image = Image.open('resources/images/milker-X-icon.png')
        imwidth = 10
        wpersent = (imwidth / float(image.size[0]))
        hsize = int(float(image.size[1]) * float(wpersent))
        image = ImageTk.PhotoImage(image.resize((imwidth, hsize), Image.ANTIALIAS))

        self.right_tree.image = image

        for item in netaddr.cidr_merge(self.right_ip_set):
            values = list()
            values.append(str(item))

            if '32' in str(item).split('/')[1]:
                values.append(False)
                values.append(1)
            else:
                values.append(True)
                values.append(len(item))

            self.right_tree.insert(
                '',
                tk.END,
                text='',
                image=image,
                values=values
            )

    def update_stats(self):
        self.intersection_set = self.left_ip_set & self.right_ip_set
        self.intersection_text_variable.set(str(len(self.intersection_set)))

        self.left_difference_set = self.left_ip_set - self.right_ip_set
        self.left_difference_text_variable.set(str(len(self.left_difference_set)))

        self.right_difference_set = self.right_ip_set - self.left_ip_set
        self.right_difference_text_variable.set(str(len(self.right_difference_set)))

    def on_double_click_left(self, event):
        try:
            selection = self.left_tree.selection()

            address_str = self.left_tree.item(selection, 'values')[0]
            self.left_ip_set.remove(address_str)
            self.left_tree.delete(selection)

            self.update_stats()
        except IndexError:
            pass

    def on_double_click_right(self, event):
        try:
            selection = self.right_tree.selection()

            address_str = self.right_tree.item(selection, 'values')[0]
            self.right_ip_set.remove(address_str)
            self.right_tree.delete(selection)

            self.update_stats()
        except IndexError:
            pass

    def export(self):
        file_name = 'ip_analyzer_results' + '_' + datetime.now().strftime('%Y-%m-%d_%H%M%S')

        workbook = xw.Workbook('output/' + file_name + '.xlsx')

        both_worksheet = workbook.add_worksheet(name='IPs in Both')
        for row, ip_range in enumerate(netaddr.cidr_merge(self.intersection_set)):
            both_worksheet.write(row, 0, str(ip_range))
        both_worksheet.set_column(0, 0, 16)

        left_worksheet = workbook.add_worksheet(name='IPs in only Left')
        for row, ip_range in enumerate(netaddr.cidr_merge(self.left_difference_set)):
            left_worksheet.write(row, 0, str(ip_range))
        left_worksheet.set_column(0, 0, 16)

        right_worksheet = workbook.add_worksheet(name='IPs in only Right')
        for row, ip_range in enumerate(netaddr.cidr_merge(self.right_difference_set)):
            right_worksheet.write(row, 0, str(ip_range))
        right_worksheet.set_column(0, 0, 16)

        workbook.close()

        if os.path.exists('output/' + file_name + '.xlsx'):
            os.system('start output/' + file_name + '.xlsx')

    def close_window(self):
        lg.info('Closing IPAnalyzerGUI window now!')
        self.master.destroy()

    @staticmethod
    def report_callback_exception(*args):
        lg.error(traceback.format_exc())
