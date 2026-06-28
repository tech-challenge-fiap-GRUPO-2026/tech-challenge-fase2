from src.llm.__main__ import build_parser, generate_text


def test_llm_cli_generates_vrp_report() -> None:
    args = build_parser().parse_args(["--generations", "2", "--population-size", "8", "--seed", "1"])

    text = generate_text(args)

    assert "Relatorio operacional da frota" in text
    assert "Veiculo" in text


def test_llm_cli_answers_tsp_question() -> None:
    args = build_parser().parse_args([
        "--mode",
        "tsp",
        "--output",
        "question",
        "--question",
        "Qual e o fitness?",
        "--generations",
        "2",
        "--population-size",
        "8",
        "--seed",
        "1",
    ])

    text = generate_text(args)

    assert "fitness" in text.lower()


def test_llm_cli_parses_openai_provider_options() -> None:
    args = build_parser().parse_args(["--provider", "openai", "--model", "custom-model"])

    assert args.provider == "openai"
    assert args.model == "custom-model"
