-- TODO: Finish implementing the calculate_fine function 
CREATE OR REPLACE FUNCTION calculate_fine()
RETURNS TRIGGER AS $$
DECLARE
    days_overdue INT;
    fine_rate DECIMAL(10, 2) := 0.50;  -- Daily fine rate
    fine_due DECIMAL(10, 2);
BEGIN
    IF NEW.return_date > NEW.due_date THEN
        -- TODO IMPLEMENT FUNCTIONALITY HERE
        days_overdue := EXTRACT(DAY FROM (NEW.return_date - NEW.due_date));
        fine_due := days_overdue * fine_rate;
        INSERT INTO fines (student_id, book_id, days_overdue, fine_due)
        VALUES (NEW.student_id, NEW.book_id, days_overdue, fine_due);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- TODO: Add CREATE TRIGGER statement here
CREATE TRIGGER trigger_calculate_fine
AFTER UPDATE OF return_date ON borrows
FOR EACH ROW
EXECUTE FUNCTION calculate_fine();