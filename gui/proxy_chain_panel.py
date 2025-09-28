from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QListWidget, QMessageBox)

class ProxyChainPanel(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.setWindowTitle("Proxy Chain Configuration")
        self.setMinimumSize(500, 350)
        self.config = config or {}
        self.proxies = self.config.get('proxy_chain', [])
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.proxy_list = QListWidget()
        self.refresh_list()
        layout.addWidget(QLabel("Proxy Chain (top = first hop):"))
        layout.addWidget(self.proxy_list)

        form = QHBoxLayout()
        self.type_box = QComboBox()
        self.type_box.addItems(["SOCKS5", "SOCKS4", "HTTP"])
        self.host_edit = QLineEdit()
        self.host_edit.setPlaceholderText("Host")
        self.port_edit = QLineEdit()
        self.port_edit.setPlaceholderText("Port")
        self.user_edit = QLineEdit()
        self.user_edit.setPlaceholderText("Username (optional)")
        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText("Password (optional)")
        form.addWidget(self.type_box)
        form.addWidget(self.host_edit)
        form.addWidget(self.port_edit)
        form.addWidget(self.user_edit)
        form.addWidget(self.pass_edit)
        layout.addLayout(form)

        btns = QHBoxLayout()
        add_btn = QPushButton("Add Proxy")
        add_btn.clicked.connect(self.add_proxy)
        del_btn = QPushButton("Remove Selected")
        del_btn.clicked.connect(self.remove_selected)
        btns.addWidget(add_btn)
        btns.addWidget(del_btn)
        layout.addLayout(btns)

    def refresh_list(self):
        self.proxy_list.clear()
        for p in self.proxies:
            desc = f"{p['type']}://{p['host']}:{p['port']}"
            if p.get('username'):
                desc += f" (user: {p['username']})"
            self.proxy_list.addItem(desc)

    def add_proxy(self):
        t = self.type_box.currentText()
        h = self.host_edit.text().strip()
        p = self.port_edit.text().strip()
        u = self.user_edit.text().strip()
        pw = self.pass_edit.text().strip()
        if not h or not p:
            QMessageBox.warning(self, "Input Error", "Host and port are required.")
            return
        proxy = {'type': t, 'host': h, 'port': p}
        if u:
            proxy['username'] = u
        if pw:
            proxy['password'] = pw
        self.proxies.append(proxy)
        self.refresh_list()
        self.host_edit.clear()
        self.port_edit.clear()
        self.user_edit.clear()
        self.pass_edit.clear()

    def remove_selected(self):
        row = self.proxy_list.currentRow()
        if row >= 0:
            del self.proxies[row]
            self.refresh_list()

    def get_proxy_chain(self):
        return self.proxies
