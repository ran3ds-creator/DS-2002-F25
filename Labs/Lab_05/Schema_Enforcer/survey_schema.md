# Survey Schema (Final, Clean)

| Column Name     | Required Data Type | Brief Description                                   |
| :-------------- | :----------------- | :-------------------------------------------------- |
| `student_id`    | `INT`              | Unique identifier for each student.                 |
| `major`         | `VARCHAR(50)`      | Student’s declared major or academic program.       |
| `GPA`           | `FLOAT`            | Grade point average on a 0.00–4.00 scale.           |
| `is_cs_major`   | `BOOL`             | True if the student is a Computer Science major.    |
| `credits_taken` | `FLOAT`            | Number of academic credits currently being taken.   |
