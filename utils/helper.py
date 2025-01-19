import subprocess
import os

tcl_test_timeout = 5
tcl_test_dir = "temp"
tcl_script_name = "test.tcl"
tcl_target = os.path.join(tcl_test_dir, tcl_script_name)


def write_tcl(content):
    os.makedirs(tcl_test_dir, exist_ok=True)
    with open(tcl_target, "w") as file:
        file.write(content)


def test_tcl():
    os.makedirs("temp", exist_ok=True)
    command = ["tclsh", tcl_target]
    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=tcl_test_timeout
        )
        if result.returncode == 0:
            return True
        else:
            return False
    except subprocess.CalledProcessError as e:
        return False
    except subprocess.TimeoutExpired as e:
        return False
