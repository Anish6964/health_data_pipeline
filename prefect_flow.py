from prefect import task, flow
import pandas as pd
import json


@task
def load_data(questionnaire_path, answers_path):
    """
    The function `load_data` reads and loads JSON data from two specified file paths.

    :param questionnaire_path: The `questionnaire_path` parameter is the file path to the JSON file
    containing the questionnaire data that you want to load. This function reads the JSON data from this
    file and returns it
    :param answers_path: The `answers_path` parameter in the `load_data` function is the file path to
    the JSON file containing the answers to the questionnaire. When the function is called, it will read
    the data from this file to load the answers
    :return: The function `load_data` returns two variables: `questionnaire` and `answers`.
    """
    with open(questionnaire_path, "r") as file:
        questionnaire = json.load(file)
    with open(answers_path, "r") as file:
        answers = json.load(file)
    return questionnaire, answers


@task
def transform_answers_to_df(answers):
    """
    The function `transform_answers_to_df` takes a list of answers, extracts the 'pid' and 'answers'
    data from each entry, adds the 'pid' to the 'answers' data, and returns a pandas DataFrame.

    :param answers: The `transform_answers_to_df` function is designed to transform a list
    of answers into a pandas DataFrame. However, the `pd` module is not imported in the code snippet
    provided. You will need to import pandas as pd at the beginning of your script for this function to
    work correctly
    :return: A DataFrame containing the answers data with an additional column 'pid' representing the
    participant ID.
    """
    answer_list = []
    for entry in answers:
        pid = entry["pid"]
        answer_data = entry["answers"]
        answer_data["pid"] = pid
        answer_list.append(answer_data)
    return pd.DataFrame(answer_list)


@task
def clean_data(df, question_ids):
    """
    The function `clean_data` takes a DataFrame and a list of question IDs, drops records where not all
    questions have been answered, and returns the cleaned DataFrame.

    :param df: The `df` parameter is typically a pandas DataFrame containing the data that needs to be
    cleaned.
    :param question_ids: The `question_ids` parameter is a list of question IDs that should have
    non-missing values in the DataFrame.
    :return: The cleaned DataFrame with incomplete records removed.
    """
    # Ensure all questions have been answered
    for question_id in question_ids:
        df = df[df[question_id].notna()]  # Remove records where any question is not answered

    # Further remove rows where any value is 'NA'
    df.replace('NA', pd.NA, inplace=True)
    df.dropna(inplace=True)

    return df


@task
def save_data(df, output_path):
    """
    The function `save_data` saves a DataFrame to a CSV file at the specified output path and prints a
    message confirming the completion of data processing.

    :param df: In the `save_data` function provided, the DataFrame `df` is being saved to a CSV file
    :param output_path: The `output_path` parameter is the file path where the cleaned data will be
    saved after processing. It is the location where the CSV file containing the cleaned data will be
    stored
    """
    df.to_csv(output_path, index=False)
    print(f"Data processing complete. Cleaned data saved to '{output_path}'.")


@flow
def health_study_data_pipeline():
    """
    The function `health_study_data_pipeline` processes health study data by loading, transforming,
    cleaning, and saving it.
    """
    questionnaire_path = "synthetic_questionnaire.json"
    answers_path = "synthetic_answers.json"
    output_path = "cleaned_questionnaire_data.csv"

    # Run the tasks
    questionnaire, answers = load_data(questionnaire_path, answers_path)
    df = transform_answers_to_df(answers)
    question_ids = [q["questionId"] for q in questionnaire["questions"]]
    cleaned_df = clean_data(df, question_ids)
    save_data(cleaned_df, output_path)


if __name__ == "__main__":
    health_study_data_pipeline()
