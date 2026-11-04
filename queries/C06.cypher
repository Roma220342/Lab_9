// CQ C06: Хто має оцінку нижче 5 при стажі понад 12 місяців (кандидати на навчання)? | фільтри
MATCH (e:Employee)
WHERE e.productivityScore < 5.0 AND e.tenureMonths > 12
RETURN e.name AS employee, e.productivityScore AS score, e.tenureMonths AS tenure
ORDER BY score
