create table if not exists merchants (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  business_name text not null,
  notification_email text not null,
  api_key text unique not null,
  webhook_secret text not null,
  created_at timestamptz not null default now()
);

create table if not exists payments (
  id uuid primary key,
  merchant_id uuid references merchants(id) on delete set null,
  amount numeric(18, 7) not null,
  asset text not null,
  asset_issuer text,
  recipient text not null,
  description text,
  webhook_url text,
  status text not null default 'pending',
  tx_id text,
  created_at timestamptz not null default now()
);

create index if not exists payments_status_idx on payments(status);
create index if not exists payments_merchant_idx on payments(merchant_id);
