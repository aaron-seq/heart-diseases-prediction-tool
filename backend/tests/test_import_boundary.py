"""Schema/application imports must not initialize the optional ML stack."""

import os
from pathlib import Path
import site
import subprocess
import sys


def test_app_import_does_not_require_ml_packages(tmp_path):
    code = """
import importlib.abc
import sys

blocked = {"numpy", "pandas", "tensorflow", "sklearn", "shap", "mlflow", "joblib"}
class RejectML(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in blocked:
            raise AssertionError("Unexpected ML import: " + fullname)
sys.meta_path.insert(0, RejectML())
from app.models.schemas import PatientHealthData
from app.main import app
assert app.title == "Heart Disease Prediction API"
assert not (blocked & set(sys.modules))
"""
    allowed = {"systemroot", "windir", "path", "pathext", "comspec", "systemdrive"}
    env = {k: v for k, v in os.environ.items() if k.casefold() in allowed}
    paths = [str(Path(__file__).resolve().parents[1])]
    if site.ENABLE_USER_SITE:
        paths.append(site.getusersitepackages())
    env.update(
        {
            "TEMP": str(tmp_path),
            "TMP": str(tmp_path),
            "USERPROFILE": str(tmp_path),
            "PYTHONPATH": os.pathsep.join(paths),
            "PYTHONDONTWRITEBYTECODE": "1",
        }
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stderr
