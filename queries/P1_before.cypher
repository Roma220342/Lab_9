// PROFILE 1 (до): пошук співробітника за іменем без індексу -> NodeByLabelScan
PROFILE MATCH (e:Employee) WHERE e.name = 'Бенчмарк 1999' RETURN e.id
