
su - postgres
psql


\list
\connect marketdb
\dt

select * from stockscreener_batch_run where "BBG" = 'AREVA.PA';

UPDATE public.stockscreener_batch_run
SET "isWorking" = False WHERE "BBG" = 'VIAD.PA';


select * from intraday where "bbg"='^FCHI' ORDER BY "Date" DESC LIMIT 10;

