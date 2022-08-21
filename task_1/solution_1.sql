with amount_risk as (
	select 
		pay.loan_id, 
		expected_payment_date, 
		expected_payment_amount, 
		date_paid, 
		amount_paid, 
		sum(case when loan.loan_id is null then expected_payment_amount end) over (partition by pay.loan_id order by expected_payment_date) as amount_at_risk,
		count(pay.loan_id) over (partition by pay.loan_id order by expected_payment_date) as calc_payment_frequency,
		row_number() over (partition by pay.loan_id order by expected_payment_date desc) as rn
	from payment_schedule pay
	left join loan_payment loan on loan.loan_id = pay.loan_id
	and loan.date_paid = pay.expected_payment_date
),
payment_agg as (
select 
	loan_id, 
	current_date - max(expected_payment_date) as current_days_past_due,
	max(expected_payment_date) as last_due_date,
	max(date_paid) as last_repayment_date,
	sum(amount_paid) as total_amount_paid,
	sum(expected_payment_amount) as total_amount_expected
from loan_payment lp
join payment_schedule using(loan_id)
group by 1
)

select 
	loan_id,
	borrower_id,
	date_of_release,
	term,
	loanamount,
	downpayment,
	state,
	city,
	zip_code,
	payment_frequency, -- the values here doesn't represent freqencies
	calc_payment_frequency, -- this is a count of the payment frequencies by the expected payment date
	maturity_date,
	current_days_past_due,
	last_due_date,
	last_repayment_date,
	amount_at_risk, 
	borrower_credit_score,
	null as branch, -- branch data are not provided
	null as branch_id,
	null as borrower_name,
	total_amount_paid,
	total_amount_expected
from loan
join borrower using(borrower_id)
join amount_risk using(loan_id)
join payment_agg using(loan_id)
where rn = 1