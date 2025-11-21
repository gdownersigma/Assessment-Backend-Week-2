SELECT experiment_id,
       subject_id,
       species_name AS species,
       experiment_date,
       type_name AS experiment_type,
       ROUND(((score/max_score)*100)::NUMERIC,2)::text || '%' AS score
FROM experiment
JOIN subject
USING (subject_id)
JOIN experiment_type
USING (experiment_type_id)
JOIN species
USING (species_id)
ORDER BY experiment_date DESC;