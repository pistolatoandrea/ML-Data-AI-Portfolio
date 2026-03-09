/*
    Questo è un file SQL potenziato da JINJA (il linguaggio tra parentesi graffe).
    Invece di scrivere "public.raw_bitcoin", usiamo la funzione source().
    Vantaggio: Se domani cambia il nome del DB, lo cambi solo nel file .yml, non qui.
*/

with source as (
    
    select * from {{ source('crypto_raw', 'raw_bitcoin') }}

),

cleaned as (

    select
        -- 1. Rinominiamo le colonne per renderle più chiare
        coin_id,
        vs_currency as currency,
        price,
        
        -- 2. Casting: Assicuriamoci che le date siano lette come TIMESTAMP
        -- (Postgres a volte legge tutto come testo se non stiamo attenti)
        last_updated::timestamp as last_updated_at,
        extracted_at::timestamp as ingestion_at

    from source

)

select * from cleaned