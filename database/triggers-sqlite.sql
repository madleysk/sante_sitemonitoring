-- SQLite Trigger insert or update table event to change component status on sites

DROP TRIGGER IF EXISTS on_insert_event_internet ;
CREATE TRIGGER on_insert_event_internet BEFORE INSERT ON evenements
WHEN (NEW.entite_concerne = 'internet')
BEGIN
	UPDATE sites SET internet= NEW.status_ev WHERE NEW.code_site = sites.code ;
END;
DROP TRIGGER IF EXISTS on_insert_event_isante ;
CREATE TRIGGER on_insert_event_isante BEFORE INSERT ON evenements
WHEN (NEW.entite_concerne = 'isante')
BEGIN
	UPDATE sites SET isante= NEW.status_ev WHERE NEW.code_site = sites.code ;
END;
DROP TRIGGER IF EXISTS on_insert_event_fingerprint ;
CREATE TRIGGER on_insert_event_fingerprint BEFORE INSERT ON evenements
WHEN (NEW.entite_concerne = 'fingerprint')
BEGIN
	UPDATE sites SET fingerprint= NEW.status_ev WHERE NEW.code_site = sites.code ;
END;
