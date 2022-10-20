from np_exploration_python.vscode_settings import VSCodeSettings

vscs = VSCodeSettings()
if not vscs.sqltools_config_exists:
    vscs.set_sqltools_default()
vscs.set_sqltools_username()
vscs.save()
