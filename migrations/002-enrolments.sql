CREATE TABLE enrolments (
  user_id INTEGER NOT NULL REFERENCES users(id),
  course_id INTEGER NOT NULL REFERENCES courses(id),
  PRIMARY KEY (user_id, course_id)
);

INSERT INTO enrolments (user_id, course_id) VALUES (2, 1);
