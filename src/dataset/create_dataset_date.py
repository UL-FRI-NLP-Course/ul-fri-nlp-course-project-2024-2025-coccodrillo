import csv

periods = [
    # Giorni della settimana
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    
    # Momenti del giorno
    "morning", "afternoon", "evening", "night", "tonight", "this morning", "this afternoon", "this evening", "this night",
    
    # Today and Tomorrow
    "today", "tomorrow", "day after tomorrow", "day before yesterday", "two days", "three days", "today evening", 
    "tomorrow evening", "this morning", "this afternoon", "this night", "tonight",
    
    # "Next" and related expressions
    "next Monday", "next Tuesday", "next Wednesday", "next Thursday", "next Friday", "next Saturday", "next Sunday",
    "next week", "next month", "next year", "next quarter", "next semester", "next fiscal year", "next time", "next payday",
    "next weekend", "next Wednesday", "next Friday afternoon", "next Friday night", "next Saturday afternoon", 
    "next Saturday night", "next Sunday morning", "next Sunday evening", "next Monday afternoon", "next Monday evening",
    "next Tuesday morning", "next Tuesday night", "next Wednesday morning", "next Wednesday evening", "next Thursday afternoon",
    "next Thursday night", "next Friday morning", "next Saturday morning", "next Sunday night",
    
    # "This" and related expressions
    "this week", "this month", "this year", "this quarter", "this semester", "this weekend", "this Friday", "this Wednesday",
    "this weekend", "this Monday", "this Tuesday", "this Wednesday", "this Thursday", "this Friday", "this Saturday", "this Sunday",
    
    # Last and past time expressions
    "last week", "last month", "last year", "last weekend", "last Friday", "last Wednesday", "last Monday", "last Tuesday", 
    "last Thursday", "last Saturday", "last Sunday", "weekend before last", "few days ago", "few weeks ago", 
    "few months ago", "few years ago", "yesterday", "day before yesterday", "year ago", "month ago",
    
    # Expressions of time
    "soon", "later", "while", "bit", "shortly", "soon after", "after while", "short time", 
    "moment", "few seconds", "few minutes", "hour", "few hours", "few days", "few weeks",
    "few months", "few years", "coming days", "coming week", "couple of weeks", "couple of days",
    "couple of months", "couple of years", "end of month", "beginning of month", "end of week",
    "beginning of week", "year's time", "end of year", "beginning of year",
    
    # Specific days and holidays
    "New Year", "Christmas", "Thanksgiving", "Halloween", 
    "weekend", "Monday morning", "Tuesday afternoon", "Friday evening", "Sunday night", "Thursday night", 
    "Wednesday evening", "Monday afternoon", "Tuesday night", "Wednesday morning", "Thursday morning", "Friday afternoon",
    
    # Next and future references
    "next few days", "next few weeks", "next few months", "next few years", "within next month", 
    "within next year", "next two weeks", "next two months", "next available day", "next available week", 
    "following week", "following day", "following month", "beginning of next week", "end of next week", 
    "next weekend", "next upcoming weekend", "first weekend of month", "last weekend of next month", 
    "next week Monday", "next week Friday", "next week Tuesday", "next month 1st", "next month 15th", 
    "next weekend Saturday", "next weekend Sunday", "first day of month", "second day of month", "third day of month",
    "first week of month", "last day of year", "Boxing", "first Monday of month", "last Friday of month", 
    "second Tuesday of month", "third Wednesday of month", "first day of next month", "second day of next month", 
    "third day of next month", "first week of next month", "next week Monday morning", "next week Friday evening", 
    "second day of next week", "third day of next week", "second day of next month", "third day of next month", 
    "weekend after next", "next quarter", "next semester"
]




# Creazione del file CSV
filename = "periods.csv"
with open(filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Period"])  # Intestazione della colonna
    for period in periods:
        writer.writerow([period])

print("CSV file 'periods.csv' has been created.")
