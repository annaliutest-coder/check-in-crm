build:
  - pip install -r requirements.txt
  - prisma generate
  - prisma db push --accept-data-loss
