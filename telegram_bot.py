from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import InputMediaPhoto, ReplyKeyboardMarkup
import matplotlib.pyplot as plt
from project import perform_analysis, load_data
from visualize import points_by_name, distribution_goals, points_and_goals, goals_for_vs_against
import pandas as pd
from get_team import get_team_by_rank, get_rank_by_team, get_team_by_goal_difference_rank, get_team_by_goals_for_rank
from tabulate import tabulate
import seaborn as sns

TOKEN = 'XXXXXXXXXXx'
# Define states
CHOOSING_COUNTRY, SHOWING_RANK = range(2)
CHOOSING_ACTION, SHOWING_TABLE, ASKING_RANK, SHOWING_TEAM = range(4)
CHOOSING_COUNTRY, CHOOSING_ACTION, CHOOSING_VISUALIZATION = range(3)
CHOOSING_QA, RECEIVING_INPUT = range(5, 7)




def format_dataframe(df):
    return tabulate(df, headers='keys', tablefmt='pretty', showindex=False)


def start(update, context):
    country_keyboard = [['England', 'Spain'], ['Germany', 'Italy']]
    reply_markup = ReplyKeyboardMarkup(country_keyboard, one_time_keyboard=True)

    update.message.reply_text(
        'Welcome to the Football Data Bot! Which country are you interested in?',
        reply_markup=reply_markup
    )
    return CHOOSING_COUNTRY

def analyze(update, context):
    user_data = context.user_data
    if 'country' in user_data:
        country = user_data['country']

        all_data = load_data('football_data.json')

        if country in all_data:
            league_table_json = all_data[country]['league_table']
            print("a")
            league_table = pd.read_json(league_table_json, orient='records')

            # Perform analysis for the selected country
            # Assuming perform_analysis returns a string with the results
            analysis_results = perform_analysis(league_table)
            update.message.reply_text(league_table)
        else:
            update.message.reply_text(f"No data available for {country}.")
    else:
        update.message.reply_text("Please select a country first using /start.")


def choose_country(update, context):
    country = update.message.text
    valid_countries = ['England', 'Spain', 'Germany', 'Italy']

    if country in valid_countries:
        context.user_data['country'] = country
        reply_keyboard = [['Visualization', 'Q&A']]
        update.message.reply_text(
            'How would you like to proceed with the analysis?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return CHOOSING_ACTION
    else:
        update.message.reply_text('Please choose a valid country: England, Spain, Germany, Italy')
        return CHOOSING_COUNTRY

def choose_action(update, context):
    action = update.message.text
    if action == 'Visualization':
        reply_keyboard = [['Points by Team', 'Goals Distribution'],
                          ['Points and Goals', 'Goals For vs Against']]
        update.message.reply_text(
            'Choose the visualization:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return CHOOSING_VISUALIZATION
    else:
        qa_keyboard = [['Team by Point Rank', 'Team by Goals Rank'],
                       ['Team by Goal Difference Rank', 'Rank by Team Name']]
        update.message.reply_text(
            'Choose your question:',
            reply_markup=ReplyKeyboardMarkup(qa_keyboard, one_time_keyboard=True))
        return CHOOSING_QA

def choose_visualization(update, context):
    visualization = update.message.text
    country = context.user_data['country']

    # Load the data from JSON file
    all_data = load_data('football_data.json')
    league_table_json = all_data[country]['league_table']
    league_table = pd.read_json(league_table_json, orient='records')

    if visualization == 'Points by Team':
        plot_path = points_by_name(league_table, country)
    elif visualization == 'Goals Distribution':
        plot_path = distribution_goals(league_table)
    elif visualization == 'Points and Goals':
        plot_path = points_and_goals(league_table)
    elif visualization == 'Goals For vs Against':
        plot_path = goals_for_vs_against(league_table)
    else:
        update.message.reply_text('Please select a valid visualization.')
        return choose_action(update, context)

    with open(plot_path, 'rb') as photo:
        update.message.reply_photo(photo=photo)

    return ConversationHandler.END

def handle_qa(update, context):
    question = update.message.text
    context.user_data['qa_choice'] = question

    if question in ['Team by Point Rank', 'Team by Goals Rank', 'Team by Goal Difference Rank']:
        update.message.reply_text('Please enter the rank number:')
    elif question == 'Rank by Team Name':
        update.message.reply_text('Please enter the team name:')
    else:
        update.message.reply_text('Please select a valid question.')
        return CHOOSING_QA

    return RECEIVING_INPUT

def receive_input(update, context):
    user_input = update.message.text
    qa_choice = context.user_data['qa_choice']
    country = context.user_data['country']

    all_data = load_data('football_data.json')
    league_table_json = all_data[country]['league_table']
    league_table = pd.read_json(league_table_json, orient='records')

    try:
        if qa_choice in ['Team by Point Rank', 'Team by Goals Rank', 'Team by Goal Difference Rank']:
            rank = int(user_input)
            team_name = get_team_by_rank(rank, league_table)  # Assuming this returns a string
            answer = str(team_name)
        elif qa_choice == 'Rank by Team Name':
            team_name = user_input
            rank = get_rank_by_team(team_name, league_table)
            answer = str(rank) if isinstance(rank, int) else rank
        else:
            answer = "Invalid option. Please start again."
    except ValueError:
        answer = "Please enter a valid number for rank."
    except Exception as e:
        answer = str(e)

    update.message.reply_text(answer)
    return choose_action(update, context)






def cancel(update, context):
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_COUNTRY: [MessageHandler(Filters.text & ~Filters.command, choose_country)],
            CHOOSING_ACTION: [MessageHandler(Filters.text & ~Filters.command, choose_action)],
            CHOOSING_VISUALIZATION: [MessageHandler(Filters.text & ~Filters.command, choose_visualization)],
            CHOOSING_QA: [MessageHandler(Filters.text & ~Filters.command, handle_qa)],
            RECEIVING_INPUT: [MessageHandler(Filters.text & ~Filters.command, receive_input)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
