from np_exploration_python.vscode_settings import VSCodeSettings

def test_init():
    vscs = VSCodeSettings()
    assert vscs._config.SQLTOOLS_KEY in vscs._settings.keys()
