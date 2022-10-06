class University:
    def __init__(self, file_name, max_students):
        self.students_array = []
        self.departments_all = []
        self.departments_dictionary = {}
        self.departments = []
        self.file_name = file_name
        self.max_students = max_students
        self.temp_department = ""

    def file_read(self):
        with open(self.file_name, "r") as file:
            data = file.readlines()
        return data

    @staticmethod
    def data_structuring(data):
        name, surname, physics, chemistry, math, computer_science, special_admission_exam, priority1, priority2, priority3 = data.split()
        return [f"{name} {surname}", float(physics), float(chemistry), float(math), float(computer_science), float(special_admission_exam), priority1, priority2, priority3]

    def department_list(self, departments):
        self.departments = sorted(list(set(departments)))
        return self.departments

    def department_score(self, x):
        # physics and math for the Physics department
        res = 0
        if self.temp_department == "Physics":
            res = self.compare_results(float((x[1] + x[3]) / 2), x[5])
            return -res, x[0]
        # chemistry for the Chemistry department
        elif self.temp_department == "Chemistry":
            res = self.compare_results(x[2], x[5])
            return -res, x[0]
        # math for the Mathematics department
        elif self.temp_department == "Mathematics":
            res = self.compare_results(x[3], x[5])
            return -res, x[0]
        # computer science and math for the Engineering Department
        elif self.temp_department == "Engineering":
            res = self.compare_results(float((x[4] + x[3]) / 2), x[5])
            return -res, x[0]
        # chemistry and physics for the Biotech department
        elif self.temp_department == "Biotech":
            res = self.compare_results(float((x[1] + x[2]) / 2), x[5])
            return -res, x[0]

    def sort_student_list_by_department(self):
        students_list_general = []
        for student in sorted(self.students_array, key=self.department_score):
            students_list_general.append([f"{student[0]}", student[1], student[2], student[3], student[4], student[5], student[6], student[7], student[8]])
        return students_list_general

    @staticmethod
    def compare_results(final_exams, admission_exam):
        return final_exams if final_exams >= admission_exam else admission_exam

    def priority_run(self, priority):
        n = self.max_students
        for department in self.departments:
            self.temp_department = department
            students_list_general = self.sort_student_list_by_department()
            students_list_filtered = list(filter(lambda x: x[priority] == department, students_list_general))
            for i, student in enumerate(students_list_filtered):
                if i <= n:
                    if department not in self.departments_dictionary:
                        # physics, chemistry, math, computer science
                        # physics and math for the Physics department
                        if department == "Physics":
                            self.departments_dictionary[department] = [[student[0], self.compare_results(float((student[1] + student[3]) / 2), student[5])]]
                        # chemistry for the Chemistry department
                        elif department == "Chemistry":
                            self.departments_dictionary[department] = [[student[0], self.compare_results(student[2], student[5])]]
                        # math for the Mathematics department
                        elif department == "Mathematics":
                            self.departments_dictionary[department] = [[student[0], self.compare_results(student[3], student[5])]]
                        # computer science and math for the Engineering Department
                        elif department == "Engineering":
                            self.departments_dictionary[department] = [[student[0], self.compare_results(float((student[4] + student[3]) / 2), student[5])]]
                        # chemistry and physics for the Biotech department
                        elif department == "Biotech":
                            self.departments_dictionary[department] = [[student[0], self.compare_results(float((student[1] + student[2]) / 2), student[5])]]
                        self.students_array.remove(student)
                    elif len(self.departments_dictionary[department]) < n:
                        # physics and math for the Physics department
                        if department == "Physics":
                            self.departments_dictionary[department].append([student[0], self.compare_results(float((student[1] + student[3]) / 2), student[5])])
                        # chemistry for the Chemistry department
                        elif department == "Chemistry":
                            self.departments_dictionary[department].append([student[0], self.compare_results(student[2], student[5])])
                        # math for the Mathematics department
                        elif department == "Mathematics":
                            self.departments_dictionary[department].append([student[0], self.compare_results(student[3], student[5])])
                        # computer science and math for the Engineering Department
                        elif department == "Engineering":
                            self.departments_dictionary[department].append([student[0], self.compare_results(float((student[4] + student[3]) / 2), student[5])])
                        # chemistry and physics for the Biotech department
                        elif department == "Biotech":
                            self.departments_dictionary[department].append([student[0], self.compare_results(float((student[1] + student[2]) / 2), student[5])])
                        self.students_array.remove(student)
                elif len(self.departments_dictionary[department]) > n or i > n:
                    break

    def __str__(self):
        temp_str = ""
        for key, value in self.departments_dictionary.items():
            temp_str += f"{key}\n"
            for item in sorted(value, key=lambda x: (-x[1], x[0])):
                temp_str += f"{item[0]} {item[1]}\n"
            temp_str += f"\n"
        return temp_str

    def record_file(self):
        for key, value in self.departments_dictionary.items():
            with open(f"{key.lower()}.txt", "w") as file:
                for item in sorted(value, key=lambda x: (-x[1], x[0])):
                    file.write(f"{item[0]} {item[1]}\n")


def main():
    # n integer representing the number of applicants that should be accepted to the university
    n = int(input())
    university1 = University("applicants.txt", n)
    students_list = university1.file_read()

    for student in students_list:
        university1.students_array.append(university1.data_structuring(f"{student.strip()}"))

    for student in university1.students_array:
        university1.departments_all.extend([student[6], student[7], student[8]])
    university1.departments = university1.department_list(university1.departments_all)

    for i in range(6, 9):
        university1.priority_run(i)

    print(university1)
    university1.record_file()


if __name__ == "__main__":
    main()
