# SQL COMMANDS

## Show Average Speed for each pitch type of each session of a specific player

select AVG(speed), sessionID, `Pitch Type_pitchType`
from `Captured Data` cd
join `Session` s
ON cd.sessionID = s.idSession
WHERE s.Pitcher\_\_id=101945
GROUP BY s.idSession, cd.`Pitch Type_pitchType`;
