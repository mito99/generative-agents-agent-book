from langchain_google_genai import ChatGoogleGenerativeAI

from common.reflection_manager import ReflectionManager, TaskReflector
from self_reflection.main import ReflectiveAgent


def main():
    import argparse

    from settings import Settings

    settings = Settings()

    parser = argparse.ArgumentParser(
        description="ReflectiveAgentを使用してタスクを実行します（Cross-reflection）"
    )
    parser.add_argument(
        "--task",
        type=str,
        help="実行するタスク",
        default="議事録システムのアイディアを考える",
    )
    args = parser.parse_args()

    # OpenAIのLLMを初期化
    llm1 = ChatGoogleGenerativeAI(
        model=settings.google_model, temperature=settings.temperature
    )

    # AnthropicのLLMを初期化
    llm2 = ChatGoogleGenerativeAI(
        model=settings.google_model, temperature=settings.temperature
    )

    # ReflectionManagerを初期化
    reflection_manager = ReflectionManager(file_path="tmp/cross_reflection_db.json")

    # AnthropicのLLMを使用するTaskReflectorを初期化
    anthropic_task_reflector = TaskReflector(
        llm=llm2, reflection_manager=reflection_manager
    )

    # ReflectiveAgentを初期化
    agent = ReflectiveAgent(
        llm=llm1,
        reflection_manager=reflection_manager,
        task_reflector=anthropic_task_reflector,
    )

    # タスクを実行し、結果を取得
    result = agent.run(args.task)

    # 結果を出力
    print(result)


if __name__ == "__main__":
    main()
