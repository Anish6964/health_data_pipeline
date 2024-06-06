import pandas as pd
import json


def load_data(questionnaire_path, answers_path):
    """
    The function `load_data` reads and loads JSON data from two files - a questionnaire file and an
    answers file.

    :param questionnaire_path: The `questionnaire_path` parameter is the file path to the JSON file
    containing the questionnaire data. This function reads the questionnaire data from this file
    :param answers_path: The `answers_path` parameter in the `load_data` function is the file path to
    the JSON file containing the answers to a questionnaire. This function reads the questionnaire data
    and answers data from the specified file paths and returns them as a tuple
    :return: The function `load_data` returns two variables: `questionnaire` and `answers`, which
    contain the data loaded from the respective JSON files specified by the `questionnaire_path` and
    `answers_path` parameters.
    """
    with open(questionnaire_path, "r") as file:
        questionnaire = json.load(file)

    with open(answers_path, "r") as file:
        answers = json.load(file)

    return questionnaire, answers


def transform_answers_to_df(answers):
    """
    The function `transform_answers_to_df` takes a list of answers, extracts the 'pid' and 'answers'
    data from each entry, adds the 'pid' to the 'answers' data, and returns a pandas DataFrame with the
    transformed data.

    :param answers: `transform_answers_to_df` function is designed to transform a list
    of answers into a pandas DataFrame. The `answers` parameter should be a list of dictionaries where
    each dictionary represents an entry with keys 'pid' and 'answers'. The 'pid' key should contain a
    unique identifier
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
        df = df[
            df[question_id].notna()
        ]  # Remove records where any question is not answered

    # Further remove rows where any value is 'NA'
    df.replace("NA", pd.NA, inplace=True)
    df.dropna(inplace=True)

    return df


def main():
    """
    The main function loads, transforms, cleans, and saves questionnaire data to a CSV file.
    """
    # Load data
    questionnaire, answers = load_data(
        "synthetic_questionnaire.json", "synthetic_answers.json"
    )

    # Transform answers to DataFrame
    df = transform_answers_to_df(answers)

    # Extract question IDs
    question_ids = [q["questionId"] for q in questionnaire["questions"]]

    # Clean data
    cleaned_df = clean_data(df, question_ids)

    # Save cleaned data to CSV
    cleaned_df.to_csv("cleaned_questionnaire_data.csv", index=False)

    print(
        "Data processing complete. Cleaned data saved to 'cleaned_questionnaire_data.csv'."
    )


if __name__ == "__main__":
    main()
