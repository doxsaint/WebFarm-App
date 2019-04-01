'''
    these classes handle course listing and prerequisites.
'''
import sys
sys.path.insert(0, '/home/projects/WebFarm-App/webscraping')
import websocScrape

class CourseMeeting:
    def __init__(self, time_start: 'time', time_end: 'time', quarter: str, days: str, location: str):
        self.time_start = time_start
        self.time_end = time_end
        self.quarter = quarter
        self.days = days
        self.location = location

class Course:
    def __init__(self, department, course_number):
        self.course_number = course_number
        self.department = department
        self.meetings = []

    def add_listing(self, meeting: CourseMeeting):
        self.meetings.append(meeting)

    def get_listings(self):
        return meetings

if __name__ == '__main__':
    assert(1==1)
