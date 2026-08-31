"""
Rule-Based Chatbot

A simple rule-based chatbot that greets the user, collects their name, age,
and gender, detects the current time of day, and responds with a
personalized greeting, recommendation, and motivational message using
nested if-else logic.
"""

import datetime


def get_time_of_day():
    """
    Detect the current time of day using the system clock.

    Returns:
        str: one of "morning", "afternoon", "evening", or "night".
    """
    hour = datetime.datetime.now().hour

    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def get_greeting(name, time_of_day):
    """
    Response category 1: Greeting.

    Builds a greeting that combines the user's name with the detected
    time of day.
    """
    if time_of_day == "morning":
        return f"Good morning, {name}! Hope you slept well."
    elif time_of_day == "afternoon":
        return f"Good afternoon, {name}! Hope your day is going well."
    elif time_of_day == "evening":
        return f"Good evening, {name}! Hope you had a productive day."
    else:
        return f"Hello, {name}! Burning the midnight oil, are we?"


def get_recommendation(time_of_day, age, gender):
    """
    Response category 2: Recommendation.

    Uses nested if-else conditions to combine time_of_day with an age
    group derived from age, then adjusts the closing line based on
    gender, so the recommendation changes with the combination of inputs.
    """
    # Determine age group first (outer condition)
    if age < 13:
        age_group = "child"
    elif age < 20:
        age_group = "teen"
    elif age < 60:
        age_group = "adult"
    else:
        age_group = "senior"

    # Nested if-else: time_of_day (outer) -> age_group (inner)
    if time_of_day == "morning":
        if age_group == "child":
            recommendation = "How about a healthy breakfast and some playtime before school?"
        elif age_group == "teen":
            recommendation = "A good breakfast and reviewing today's study plan would set you up well."
        elif age_group == "adult":
            recommendation = "Consider a workout or a coffee before diving into work."
        else:
            recommendation = "A light walk and a nutritious breakfast can start your day right."
    elif time_of_day == "afternoon":
        if age_group == "child":
            recommendation = "Time for a fun activity or homework session!"
        elif age_group == "teen":
            recommendation = "A good time to catch up on assignments or hobbies."
        elif age_group == "adult":
            recommendation = "Take a short break and stay hydrated during your work day."
        else:
            recommendation = "A relaxing afternoon nap or reading session might suit you."
    elif time_of_day == "evening":
        if age_group == "child":
            recommendation = "Wind down with a story or some family time."
        elif age_group == "teen":
            recommendation = "Good time to relax or catch up with friends."
        elif age_group == "adult":
            recommendation = "Consider some exercise or spending time with family."
        else:
            recommendation = "A calm evening walk could be refreshing."
    else:  # night
        if age_group in ("child", "teen"):
            recommendation = "It's getting late, time to wind down and get some sleep!"
        else:
            recommendation = "Try to wrap up and get some rest for tomorrow."

    # Inner condition based on gender, tweaks the closing line
    gender_normalized = gender.strip().lower()
    if gender_normalized in ("female", "f"):
        recommendation += " Take care of yourself!"
    elif gender_normalized in ("male", "m"):
        recommendation += " Take care, champ!"
    else:
        recommendation += " Take care!"

    return recommendation


def get_motivational_message(age):
    """
    Response category 3: Motivational message.

    Chooses a motivational message based on the user's age group.
    """
    if age < 13:
        return "Keep exploring and learning new things every day!"
    elif age < 20:
        return "Your future is bright, stay curious and work hard!"
    elif age < 60:
        return "Every step you take today builds the life you want tomorrow."
    else:
        return "Wisdom and experience are your greatest strengths, keep inspiring others!"


def run_test_scenarios():
    """
    Step 7: Test the chatbot with five different input scenarios
    (name, age, gender, time_of_day) and print the responses so we can
    verify they change appropriately across scenarios.
    """
    scenarios = [
        ("Aditi", 9, "female", "morning"),
        ("Rahul", 17, "male", "afternoon"),
        ("Sam", 34, "other", "evening"),
        ("Meena", 67, "female", "night"),
        ("Vikram", 45, "male", "morning"),
    ]

    print("=== Running Test Scenarios ===\n")
    for i, (name, age, gender, time_of_day) in enumerate(scenarios, start=1):
        print(f"Scenario {i}: name={name}, age={age}, gender={gender}, time_of_day={time_of_day}")
        print(get_greeting(name, time_of_day))
        print(get_recommendation(time_of_day, age, gender))
        print(get_motivational_message(age))
        print("-" * 50)


def main():
    """
    Main driver function.

    Greets the user, collects name, age, and gender, automatically
    detects the current time of day, and prints the combined
    greeting, recommendation, and motivational message.
    """
    print("Welcome to the Rule-Based Chatbot!")

    name = input("What is your name? ").strip() or "Friend"

    # Validate age input so the program doesn't crash on bad input
    while True:
        age_input = input("What is your age? ").strip()
        if age_input.isdigit():
            age = int(age_input)
            break
        print("Please enter a valid number for age.")

    gender = input("What is your gender (male/female/other)? ").strip()

    time_of_day = get_time_of_day()

    print("\n" + get_greeting(name, time_of_day))
    print(get_recommendation(time_of_day, age, gender))
    print(get_motivational_message(age))


if __name__ == "__main__":
    # Verify the rule-based logic works correctly across several scenarios
    run_test_scenarios()

    # Then run the real interactive chatbot session
    main()


# ---------------------------------------------------------------------------
# Observations
# ---------------------------------------------------------------------------
# - Using datetime.now().hour to detect time of day is simple and reliable,
#   but it depends entirely on the system clock, so it can't distinguish
#   "morning" and "night" the way a human would if the clock is wrong or
#   the machine is in a different timezone than the user.
# - Nesting if-else on two dimensions (time_of_day, then age_group) made the
#   recommendation logic combinatorial fast: 4 time periods x 4 age groups
#   already gives 16 branches. This is manageable here, but a real chatbot
#   would likely replace this with a lookup table/dictionary or a small
#   rules engine as more categories are added.
# - Splitting the logic into small functions (get_time_of_day,
#   get_greeting, get_recommendation, get_motivational_message) made it
#   possible to test the "brain" of the chatbot (run_test_scenarios) without
#   needing interactive input(), which is a useful pattern for testing any
#   input()-driven CLI program.
# - The five test scenarios confirmed that responses do change appropriately
#   with each input combination: greetings change with time_of_day, the
#   recommendation changes with both time_of_day and age_group, and the
#   motivational message changes with age.
