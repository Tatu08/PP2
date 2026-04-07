CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    INSERT INTO phonebook (name, phone) 
    VALUES (p_name, p_phone)
    ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_contacts(p_names VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INTEGER;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9+]+$' THEN
            INSERT INTO phonebook(name, phone) VALUES(p_names[i], p_phones[i])
            ON CONFLICT (name) DO UPDATE SET phone = EXCLUDED.phone;
        ELSE
            RAISE NOTICE 'Қате дерек жіберілмеді: %, %', p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_search VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook 
    WHERE name = p_search OR phone = p_search;
END;
$$;