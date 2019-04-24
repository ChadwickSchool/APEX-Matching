# About
APEX student-project matching
A project for Ms. White (whoever has to assign students to projects)  by students from Post-AP Computer Science: Intro to Software Engineering
A generic group maker and group checker
Project intended to help Ms. White have an easier time Matching Students to their preferred APEX project

Created by Michael Huang

# Requirements
- Virtual Box
- Ubuntu Vagrant
- Unix based Command Line Utility

# Setup
- If no Vagrant file exists, put the Ubuntu Vagrant file in the root project director (If one already exists skip this step)
- Open your Command Line Utility
1. Navigate to the root project file (has the Vagrant file) type `vagrant up`
2. Type 'vagrant ssh'
3. Navigate inside the project directory `cd /vagrant/project/`
4. If there is a already a `database.db` delete it
5. Run `create_projects.py`
6. Run `create_prefs.py`

# Configure Database (Optional if integrating into another program)
1. Modify `create_projects.py` and `create_prefs` by filling all fields appropriately
3. Those who have no preference leave preferences blank.
4. Only have as many `Students` as you actually have`

# Run Example
1. In `algorithm.py`
- Change how many `MAX_STUDS_PER_GROUP` each project should have on line 17
  - Change how many `MIN_STUDS_PER_GROUP` each project should have on line 18
  * note that if MAX is too small and/or MIN is too large there will be a lot of unmatched students
2. run `algorithm.py`

# Integration
- Can run off of an existing database
- Recommend that `prefs` and `projects` are set by an outside UI
- Methods from `algorithm.py` need to be used in the order of the example

# Check Existing Trip
1. Trips should be in this format
  - A `Trip` is a `List` of `Group`
  - A `Group` is a `List` of `Student_class`
2. From `improved_algorithm_interface.py` Run
  1. `unassigned_students(YOUR_TRIP)`
  2. `print_stats(YOUR_TRIP)`

# Database Object Definitions
- `Project` 
  - `id` an auto generated id number
  - `name` the name of the project
  - `session_number` the session which the project is being presented in
  - `raw_score` the raw score of a project
     - `raw_score` is defined by the total number of students who want to watch the project
  - `pop_score` the popularity score of a project
     - `pop_score` is defined as the weighted score of each project, where every first preference counts as 4 points, second preference as 3, third as 2, and fourth as 1
  - `students` the list of students assigned to the project
- `Student`
  - `id` an auto generated id number
  - `name` the student's first and last name, seperated with a space
  - `project` the project(s) in which the student is assigned
- `Pref`
  - `id` an auto generated id number
  - `name` the name of the preferred project

# Group Assignment Explanation
- Key Requirements

Each student can provide a list of preferences. (Everybody must either have X preferences or 0 preferences)
Each group should be gender balanced as close as possible
The algorithm should ensure that each student is matched into a group with at least one preference (if they provided the maximum number of preferences).  

- Algorithm Theory

Our algorithm will maximize the chance of a everyone being matched with at least one of their preference and possibly more.

The basic idea is that the best chance someone has to be matched into a group with one of their preferences is to “choose” which group to join, where the groups contain people who have preferred them the most (ie popular people).  Conversely, if groups are filled with people who are not highly preferred then the likelihood of joining a group with a preference is reduced.


For example, if Joan who has only one person who has her as a preference and she is pulled into a group early in the process, then she has to hope that one of her
preferences joins her group because that preference prefers someone else in her group.  She is hoping for a coincidence to occur.  Therefore, it is more ideal if she can choose a group towards the end of the process, when most other people are already assigned to almost ensure she will at least be matched with one preference.  

Conversely, for example, if John has many people who have he as a preference and John is assigned early in the process, then Johns creates more opportunities for people to join his group and match with a preference.

So in summary, the basic idea is to assign high preferred (popular) people to groups early in the process and assign lower preferred (less popular) people to
How the algorithm works
Calculate a preference score (pref-score)
The pref-score is the number of other students who have listed the student as a preference

- Calculate a mutual score (mutual-score)
The mutual-score is the number of preferences who have also listed the person as a preference.  For example, if Joan’s preferences include John, Sally, and Jennifer; and John and Jennifer also have Joan as a preference, then Joan’s mutual-score is 2.  The idea is to add people to the list early in the process to make room for others to choose their groups if possible.

- Sort the students by pref-score and mutual-score
Assigning students to groups in the order of pref-score and mutual-score will create more opportunities for lower pref-score students to choose their groups.

- Assign each student according to the algorithm theory
Students will be assigned to groups attempting to keep the groups balanced in size through the assignment process to maximize opportunities for students to choose their way into groups and therefore maximizing their chance for a preference match.

- Students who are pulled into groups will be selected based on highest pref-score while students who choose a group will choose the lowest group with a preference with the lowest pref-score.  

Here is a summary of the algorithm logic to when assigning each student to a group:

- If assigned to a group already						
 - Already Assigned With A Preference - If assigned to a group with a pref then do nothing and move to assign next student
 - Pull Highest Pref-score Preference Into Group - If any prefs not assigned, assign (pull) pref with highest pref-score to join the students assigned group if gender-limit permits 	
 - Cannot Be Matched - if all prefs assigned to other groups then this person does get a preference… add them to open groups at the end of the assignment process

- If not assigned to a group already					
  Find the least crowded group(s) (from left to right)			
  - Join Smallest Group With A Preference - If there is a preference in the smallest group, assign the person to this group, if gender-limit permits
  - Join Smallest Group With Lowest Pref-Score Preference - If there are multiple smallest groups, then assign to the group with a pref with the lowest pref-score, if gender-limit permits
  - Join Smallest Group along with Highest Pref-score Preference - if there is no preference in the smallest group(s) then assign the person to the smallest group, and pull into the group the preference with the highest pref-score (who is not yet assigned) and has a preferences-remaining > 1, if gender-limit permits
  - Join Smallest Group With Lowest Pref-Score Preference - otherwise, if the pref's preferences-remaining <=1 then assign the person to next smallest group which contains the lowest pref-score), if gender-limit permits
  - Join Smallest Group With Lowest Pref-Score Preference - But if all preferences are assigned (ie there aren't any to pull along) then choose the smallest group with a preference; and if there are multiple smallest groups choose the group with a pref with the lowest pref-score, if gender-limit permits
