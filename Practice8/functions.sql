CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.name, c.phone FROM phonebook c
    WHERE c.name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit INTEGER, p_offset INTEGER)
RETURNS TABLE(name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.name, c.phone FROM phonebook c
    ORDER BY c.name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;