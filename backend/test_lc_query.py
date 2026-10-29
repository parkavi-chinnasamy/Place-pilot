import json
import urllib.request
import urllib.error

def test_fetch(username: str):
    url = "https://leetcode.com/graphql"
    query = """
    query getUserProfile($username: String!) {
        matchedUser(username: $username) {
            username
            githubUrl
            profile {
                ranking
                userAvatar
                realName
                reputation
            }
            submitStatsGlobal {
                acSubmissionNum {
                    difficulty
                    count
                    submissions
                }
            }
            userCalendar {
                streak
                totalActiveDays
                submissionCalendar
            }
        }
        userContestRanking(username: $username) {
            attendedContestsCount
            rating
            globalRanking
            totalParticipants
            topPercentage
        }
    }
    """
    
    payload = {
        "query": query,
        "variables": {"username": username}
    }
    data = json.dumps(payload).encode("utf-8")
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://leetcode.com/{username}/"
    }
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            res_json = json.loads(body)
            print("Status:", resp.status)
            matched = res_json.get("data", {}).get("matchedUser")
            contest = res_json.get("data", {}).get("userContestRanking")
            print("Matched user found:", matched is not None)
            if matched:
                print("Username:", matched.get("username"))
                print("Global ranking:", matched.get("profile", {}).get("ranking"))
                print("Stats:", matched.get("submitStatsGlobal", {}).get("acSubmissionNum"))
                print("Calendar streak:", matched.get("userCalendar", {}).get("streak"))
                print("Calendar totalActiveDays:", matched.get("userCalendar", {}).get("totalActiveDays"))
            if contest:
                print("Contest rating:", contest.get("rating"))
                print("Contest count:", contest.get("attendedContestsCount"))
                print("Top percentage:", contest.get("topPercentage"))
            else:
                print("Contest: Unrated (None)")
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    print("--- Testing 'tourist' ---")
    test_fetch("tourist")
    print("\n--- Testing non-existent user ---")
    test_fetch("this_user_definitely_does_not_exist_98127391823")
