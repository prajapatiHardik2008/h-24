import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_github_data(username):
    # GitHub Public API URL
    url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos"
    
    # User profile data fetch karna
    user_data = requests.get(url).json()
    # Repositories data fetch karna
    repos_data = requests.get(repos_url).json()
    
    if 'message' in user_data and user_data['message'] == 'Not Found':
        print("User nahi mila! Username check karein.")
        return None

    print(f"--- Profile: {user_data['name']} ---")
    print(f"Followers: {user_data['followers']}")
    print(f"Public Repos: {user_data['public_repos']}")
    
    # Data ko table (DataFrame) mein convert karna
    repo_list = []
    for repo in repos_data:
        repo_list.append({
            'Name': repo['name'],
            'Stars': repo['stargazers_count'],
            'Language': repo['language'] if repo['language'] else "None",
            'Forks': repo['forks_count']
        })
    
    df = pd.DataFrame(repo_list)
    return df

# Apna GitHub username yahan likhein
username = "prajapati-hardik-24" # Aapka GitHub ID
df = get_github_data(username)

if df is not None:
    print("\n--- Aapki Repositories ki Table ---")
    print(df)

    # Graph: Top Languages used in Repos
    df['Language'].value_counts().plot(kind='pie', autopct='%1.1f%%', figsize=(8, 6))
    plt.title(f"Languages used by {username}")
    plt.ylabel('') # Y-axis label hatane ke liye
    plt.show()