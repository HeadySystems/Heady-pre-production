import json

import src.process_data as process_data


def test_mean_pool_2d() -> None:
    matrix = [[1, 2, 3], [4, 5, 6]]
    assert process_data._mean_pool_2d(matrix) == [2.5, 3.5, 4.5]


def test_pool_feature_extraction_output_single() -> None:
    output = [[[1.0, 2.0], [3.0, 4.0]]]
    pooled = process_data._pool_feature_extraction_output(output)
    assert pooled == [[2.0, 3.0]]


def test_qa_interface_truncates_inputs(monkeypatch) -> None:
    def fake_generate(prompt, model=None, parameters=None, options=None):
        return {"model": model, "output": "ok", "raw": {}}

    monkeypatch.setattr(process_data, "hf_generate", fake_generate)
    monkeypatch.setattr(process_data, "HEADY_QA_TRUNCATE_INPUTS", True)
    monkeypatch.setattr(process_data, "HEADY_QA_MAX_QUESTION_CHARS", 5)
    monkeypatch.setattr(process_data, "HEADY_QA_MAX_CONTEXT_CHARS", 5)

    result = process_data.qa_interface("question-too-long", "context-too-long")
    assert result["ok"] is True
    assert result["answer"] == "ok"


def test_health_check_output(monkeypatch, capsys) -> None:
    monkeypatch.setattr(process_data, "HF_TOKEN", "token")
    try:
        process_data.handle_health_check()
    except SystemExit:
        pass
    captured = json.loads(capsys.readouterr().out)
    assert captured["status"] == "healthy"
