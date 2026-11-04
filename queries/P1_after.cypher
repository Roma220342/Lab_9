// PROFILE 1 (після): той самий запит з індексом employee_name -> NodeIndexSeek
PROFILE MATCH (e:Employee) WHERE e.name = 'Бенчмарк 1999' RETURN e.id
