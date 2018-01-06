UPDATE public.stockscreener_batch_run
SET "mnemo" = null WHERE "mnemo" = 'tt';




select * from spots where "bbg"='BOI.PA' and "Date"='2017-10-07' LIMIT 10;

UPDATE public.spots
SET "Close" = 78.39 WHERE "bbg"='BOI.PA' and "Date"='2017-10-07';

 bbg | Open | High | Low | Close | Volume | Adj Close | Date 

INSERT INTO public.spots VALUES
('BOI.PA', 78.50, 78.50, 78.30, 78.39, 866, 78.39, '2017-10-06');

INSERT INTO public.spots VALUES
('BOL.PA', 4.13, 4.157, 4.114, 4.114, 1214160, 4.114, '2017-10-06');
6/10/2017	4,13	4,157	4,114	4,114	1.214.160	