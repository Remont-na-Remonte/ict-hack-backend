# Generated by Django 3.1.3 on 2020-12-21 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('code', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('endDate', models.DateField()),
                ('KBK', models.DecimalField(decimal_places=0, max_digits=21)),
                ('paymentYearMonth', models.DateField()),
                ('paymentSumRUR', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.CharField(editable=False, max_length=30, primary_key=True, serialize=False)),
                ('contratUrl', models.URLField()),
                ('documentBase', models.CharField(max_length=1024)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('fz', models.SmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('printFromUrl', models.URLField()),
                ('protocolDate', models.DateField()),
                ('publishDate', models.DateField()),
                ('regionCode', models.SmallIntegerField()),
                ('scanUrld', models.URLField()),
                ('signDate', models.DateField()),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.budget')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('inn', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('fullName', models.CharField(max_length=512)),
                ('kpp', models.IntegerField()),
                ('postalAddress', models.CharField(max_length=512)),
                ('regNum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Road',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25)),
                ('road_title', models.CharField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mk', models.IntegerField()),
                ('section_start', models.IntegerField()),
                ('section_end', models.IntegerField()),
                ('coordinates', models.JSONField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('inn', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('kpp', models.IntegerField()),
                ('factualAddress', models.CharField(max_length=1024)),
                ('organizationName', models.CharField(max_length=1024)),
                ('singularName', models.CharField(max_length=1024)),
                ('middleName', models.CharField(max_length=25)),
                ('lastName', models.CharField(max_length=25)),
                ('firstName', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Section_Road',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('road', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.road')),
                ('selection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.section')),
            ],
        ),
        migrations.AddField(
            model_name='road',
            name='selections',
            field=models.ManyToManyField(through='contracts.Section_Road', to='contracts.Section'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('sid', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1024)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('contract_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.CharField(editable=False, max_length=30, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('region', models.SmallIntegerField()),
                ('signDate', models.DateField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
            ],
        ),
        migrations.CreateModel(
            name='Contract_Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Contract_Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contracts.customer')),
            ],
        ),
        migrations.AddField(
            model_name='contract',
            name='customers',
            field=models.ManyToManyField(related_name='customer_contract_type', through='contracts.Contract_Customer', to='contracts.Customer'),
        ),
        migrations.AddField(
            model_name='contract',
            name='suppliers',
            field=models.ManyToManyField(through='contracts.Contract_Supplier', to='contracts.Customer'),
        ),
    ]
