import subprocess
import time

from atomacos.AXKeyCodeConstants import COMMAND, SHIFT


def calculate_center(size, position):
    center = (position.x + size.width / 2, position.y + size.height / 2)
    return center


def test_click_and_enter(finder_app):
    fields = finder_app.textFieldsR("*search*")
    field = fields[0]
    center_position = calculate_center(field.AXSize, field.AXPosition)
    field.clickMouseButtonLeft(center_position)
    field.sendKeys("hello")
    time.sleep(1)
    assert field.AXValue == "hello"


def test_drag_folders(finder_app):
    test_path = "~/Desktop/test_input"

    subprocess.call("rm -rf {}".format(test_path), shell=True)
    subprocess.call("mkdir {}".format(test_path), shell=True)

    finder_app.sendKeyWithModifiers("g", modifiers=[COMMAND, SHIFT])

    end_time = time.time() + 10
    while (
        not finder_app.findFirstR(AXRole="AXButton", AXTitle="Go")
        and time.time() < end_time
    ):
        time.sleep(0.1)

    finder_app.sendKeys(test_path + "\n")

    while (
        finder_app.findFirstR(AXRole="AXButton", AXTitle="Go")
        and time.time() < end_time
    ):
        time.sleep(0.1)

    finder_app.sendKeyWithModifiers("n", modifiers=[COMMAND, SHIFT])
    finder_app.sendKeys("helloworld\n")

    finder_app.sendKeyWithModifiers("n", modifiers=[COMMAND, SHIFT])
    finder_app.sendKeys("helloworld2\n")

    file1 = finder_app.findFirstR(AXFilename="helloworld")
    file2 = finder_app.findFirstR(AXFilename="helloworld2")

    def center_position(ref):
        pos = ref.AXPosition
        size = ref.AXSize
        return pos.x + size.width / 2, pos.y + size.height / 2

    finder_app.dragMouseButtonLeft(center_position(file2), center_position(file1))

    output = subprocess.check_output(
        "ls {}/helloworld".format(test_path), shell=True, universal_newlines=True
    )
    assert "helloworld2" in output