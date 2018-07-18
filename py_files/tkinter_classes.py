import logging as lg
import traceback


class IPAnalyzerGUI():
    def __init__(self, master):
        self.master = master
        master.title('AssetViewer')
        # self.master.geometry('1000x500')
        self.master.protocol('WM_DELETE_WINDOW', self.close_window)
        self.master.option_add('*tearOff', 'FALSE')
        self.master.report_callback_exception = self.report_callback_exception

        # Declare GUI Variables
        self.asset_object_list = asset_object_list
        self.attributes = PurgeAsset.attributes
        self.qualys_asset_object_set = set()
        self.input_lines = str()
        self.trees = list()
        self.tree_names = list()

        # Declare GUI Components
        self.main_frame = tk.Frame(self.master)

        self.notebook = ttk.Notebook(self.main_frame)

        self.good_match_tree_tab = ttk.Frame(self.notebook)
        self.bad_match_tree_tab = ttk.Frame(self.notebook)
        self.no_entries_tree_tab = ttk.Frame(self.notebook)

        self.good_match_tree = ttk.Treeview(self.good_match_tree_tab)
        self.bad_match_tree = ttk.Treeview(self.bad_match_tree_tab)
        self.no_match_tree = ttk.Treeview(self.no_entries_tree_tab)

        self.good_match_tree_tab_vsb = ttk.Scrollbar(self.good_match_tree_tab)
        self.good_match_tree_tab_hsb = ttk.Scrollbar(self.good_match_tree_tab)
        self.trees.append(self.good_match_tree)
        self.tree_names.append('good_match_tree')

        self.bad_match_tree_tab_vsb = ttk.Scrollbar(self.bad_match_tree_tab)
        self.bad_match_tree_tab_hsb = ttk.Scrollbar(self.bad_match_tree_tab)
        self.trees.append(self.bad_match_tree)
        self.tree_names.append('bad_match_tree')

        self.no_match_tree_tab_vsb = ttk.Scrollbar(self.no_entries_tree_tab)
        self.no_match_tree_tab_hsb = ttk.Scrollbar(self.no_entries_tree_tab)
        self.trees.append(self.no_match_tree)
        self.tree_names.append('no_match_tree')

        self.main_label = tk.Label(self.main_frame)
        self.submit_button = tk.Button(self.main_frame)

        # Customize GUI Components
        self.configure_components()

        # Grid Components
        self.grid_components()

        # Other Methods
        self.fill_tree()

        self.master.lift()

    def close_window(self):
        lg.info('Closing IPAnalyzerGUI window now!')
        self.master.destroy()

    @staticmethod
    def report_callback_exception():
        lg.error(traceback.format_exc())
