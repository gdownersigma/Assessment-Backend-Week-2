SELECT species_name,
       experiment_id,
       is_predator,
       CASE
           WHEN is_predator = 't' 
                THEN ROUND((score*1.2)::NUMERIC,1) 
           ELSE score
       END AS score
FROM subject
JOIN experiment
USING (subject_id)
JOIN species
USING (species_id)
ORDER BY score DESC;
