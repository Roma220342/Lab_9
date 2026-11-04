// ЛР 9, результат 2, крок 4: навмисне порушення обмеження унікальності.
// Очікувано: Neo.ClientError.Schema.ConstraintValidationFailed
// «Node(..) already exists with label `Employee` and property `id` = 'petro'»
CREATE (:Employee {id: 'petro', name: 'Дублікат Петра'});

// Друге порушення — неунікальний табельний номер:
CREATE (:Employee {id: 'dup_e003', employeeId: 'E-003', name: 'Дублікат E-003'});
