#Libraries

import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt 


script_dir = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(script_dir, "cowboys_stats.db")

def analyze_player_stats():
    """
    Connects to the SQLite database, analyzes player stats using Pandas,
    and prints the results.
    """
    try:
        #Connect to the SQLite database
        conn = sqlite3.connect(DB_FILE)
   

  
        dak_stats_df = pd.read_sql_query("SELECT * FROM DakStats", conn)
        game_df = pd.read_sql_query("SELECT * FROM Game", conn)
        player_df = pd.read_sql_query("SELECT * FROM Player", conn)

        #Data Cleaning
        dak_player_id = player_df[player_df['name'] == 'Dak Prescott']['player_id'].iloc[0]
        dak_stats_df = dak_stats_df[dak_stats_df['player_id'] == dak_player_id]
        merged_df = pd.merge(dak_stats_df, game_df, on="game_id")

        # Question 1
        print("\n--- Question 1: What are Dak Prescott's average stats? ---\n")
        total_yards = merged_df['yards'].sum()
        total_completions = merged_df['completions'].sum()
        total_attempts = merged_df['attempts'].sum()
        total_games = len(merged_df)
        avg_yards_per_game = total_yards / total_games
        completion_percentage = (total_completions / total_attempts) * 100 if total_attempts > 0 else 0
        print(f"Dak Prescott's Season Averages:")
        print(f"  - Average Passing Yards per Game: {avg_yards_per_game:.2f}")
        print(f"  - Overall Completion Percentage: {completion_percentage:.2f}%")

        # Question 2
        print("\n--- Question 2: What was Dak Prescott's best game by passing yards? ---\n")
        best_game = merged_df.sort_values(by='yards', ascending=False).iloc[0]
        print(f"Dak Prescott's best performance was against the {best_game['opponent']} on {best_game['game_date']}.")
        print(f"  - Passing Yards: {best_game['yards']}")
        print(f"  - Game Result: {best_game['result']}")

    #Math Plot Lib/Creating Graph

       
        merged_df = merged_df.sort_values(by='game_date')

        plt.figure(figsize=(12, 7))  
        
        
        plt.bar(merged_df['opponent'], merged_df['yards'], color='dodgerblue', edgecolor='black')

        
        plt.title("Dak Prescott's Passing Yards per Game", fontsize=16)
        plt.xlabel("Opponent", fontsize=12)
        plt.ylabel("Passing Yards", fontsize=12)
        plt.xticks(rotation=45, ha="right") 
        plt.grid(axis='y', linestyle='--', alpha=0.7) 
        plt.tight_layout()  

        # Saving the image
        plot_filename = os.path.join(script_dir, 'dak_yards_per_game.png')
        plt.savefig(plot_filename)
        
        
        # Created a Error catcher to help identify issues with the analsyis.
    except sqlite3.Error as e:
        print(f" Database error: {e}")
    except FileNotFoundError:
        print(f" Error: The database file '{DB_FILE}' was not found.")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            

if __name__ == "__main__":
    analyze_player_stats()