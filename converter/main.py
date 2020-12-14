from converter.app import flask_app
from converter.pydoc_install_module import install_pandoc
import converter.view

if __name__ == '__main__':
    install_pandoc()
    flask_app.run()
