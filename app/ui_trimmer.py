import re

from nicegui import ui


@ui.page("/trimmer")
def trimmer_page():
    ui.label("Response Trimmer").style(
        "font-size:2rem; font-weight:bold; margin-bottom:1rem;"
    )
    with ui.row():
        pattern_input = (
            ui.input("Regex Pattern")
            .props('placeholder="Contoh: \\d+"')
            .style("width:300px")
        )
    with ui.row():
        input_area = (
            ui.textarea("Input Text")
            .props("autogrow")
            .style("width:400px; height:200px")
        )
        result_area = (
            ui.textarea("Result Text")
            .props("autogrow readonly")
            .style("width:400px; height:200px")
        )

    def update_result():
        pattern = pattern_input.value or ""
        text = input_area.value or ""
        try:
            if pattern:
                result = "\n".join(re.findall(pattern, text))
            else:
                result = text
        except Exception as e:
            result = f"Error: {e}"
        result_area.value = result

    pattern_input.on("input", lambda e: update_result())
    input_area.on("input", lambda e: update_result())

    ui.label("Masukkan regex pattern dan teks, hasil akan muncul otomatis.").style(
        "margin-top:1rem; color:gray"
    )


if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
