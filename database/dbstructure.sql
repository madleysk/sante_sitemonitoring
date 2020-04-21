
-- Trigger insert or update table event record on mailbox_trash tables
--

delimiter $$
DROP TRIGGER IF EXISTS on_update_event ;
$$
CREATE TRIGGER on_update_event BEFORE INSERT ON evenements
FOR EACH ROW
BEGIN
	IF (NEW.entite_concerne = 'internet') THEN UPDATE sites SET internet= NEW.status_ev WHERE NEW.code_site = sites.code ;
	ELSEIF (NEW.entite_concerne = 'isante') THEN UPDATE sites SET isante= NEW.status_ev WHERE NEW.code_site = sites.code;
	ELSEIF (NEW.entite_concerne = 'fingerprint') THEN UPDATE sites SET fingerprint= NEW.status_ev WHERE NEW.code_site = sites.code;
	END IF;
END;$$
delimiter ;


