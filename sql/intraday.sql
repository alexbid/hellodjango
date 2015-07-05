﻿

SELECT "toto", "Last" FROM
(SELECT "Last", MAX("Date") AS toto FROM intraday WHERE ("Date" BETWEEN '2015-07-01 00:00:00' AND '2015-07-01 23:00:00') GROUP BY "Last")
AS DERIVEDTABLE ORDER BY "toto" ASC