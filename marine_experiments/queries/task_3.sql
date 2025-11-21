SELECT type_name,
       species_name,
       ROUND(AVG(score),1) AS round
FROM experiment
JOIN experiment_type
USING (experiment_type_id)
JOIN subject
USING (subject_id)
JOIN species
USING (species_id)
GROUP BY type_name,species_name
HAVING ROUND(AVG(score),1) > 5;