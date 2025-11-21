SELECT subject_id,
       subject_name,
       species_name,
       TO_CHAR(date_of_birth,'YYYY-MM') AS date_of_birth
FROM subject
JOIN species
USING(species_id)
ORDER BY date_of_birth DESC;

