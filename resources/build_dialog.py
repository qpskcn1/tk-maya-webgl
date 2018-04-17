__author__ = 'yi'

from subprocess import check_output

UI_PYTHON_PATH = "../python/tk_maya_webgl/ui"


def build_ui(ui_name):
    print "Building UI: %s" % ui_name
    out = check_output(
        [
            'pyside-uic',
            '--from-imports',
            '%s.ui' % ui_name
        ]
    )
    amended_out = out.replace("from PySide import", "from tank.platform.qt import")
    with open("%s/%s.py" % (UI_PYTHON_PATH, ui_name), "w") as f:
        f.write(amended_out)


def build_res(res_name):
    print "Building Resource: %s" % res_name
    out = check_output(
        [
            "C:/Python27/Lib/site-packages/PySide/pyside-rcc",
            "%s.qrc" % res_name
        ]
    )
    amended_out = out.replace("from PySide import", "from tank.platform.qt import")
    with open("%s/%s_rc.py" % (UI_PYTHON_PATH, res_name), "w") as f:
        f.write(amended_out)


if __name__ == "__main__":
    print "Start..."
    build_ui('dialog')
    # build_res('resources')
    print "Done!"