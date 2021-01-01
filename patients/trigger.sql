CREATE OR REPLACE FUNCTION trigger_update_state()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
AS
$$
BEGIN
    if new.state <> old.state then
        insert into state_log (report, state_old, state_new) VALUES (new.id, old.state, new.state);
    end if;
    return new;
END;
$$;

drop trigger CHANGE_REPORT_STATE on report;
create trigger CHANGE_REPORT_STATE
    after update
    on report
    for each row
execute procedure trigger_update_state()