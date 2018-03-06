pragma solidity ^0.4.0;

contract P2PLending {
    // Global Variables
    mapping (address => uint) balances; // Either investor or borrower => balance

    mapping (address => Investor) investors; // Investor public key => Investor
    mapping (address => Borrower) borrowers; // Borrower public key => Borrower
    // address[] investorArray;
    // address[] borrowerArray;

    //Global counters, always increment
    uint public numApplications;
    uint public numLoans;

    mapping (uint => LoanApplication) public applications;
    mapping (uint => Loan) public loans;

    mapping(address => bool) hasOngoingLoan;
    mapping(address => bool) hasOngoingApplication;
    mapping(address => bool) hasOngoingInvestment;

    // Structs
    struct Investor{
        address investor_public_key;
        string name;
        bool EXISTS;
    }

    struct Borrower{
        address borrower_public_key;
        string name;
        bool EXISTS;
    }

    struct LoanApplication{
        //For traversal and indexing
        bool openApp;
        uint applicationId;

        address borrower;
        uint duration; // In months
        uint credit_amount; // Loan amount
        uint interest_rate; //From form
        string otherData; // Encoded string with delimiters (~)

    }

    struct Loan{

        //For traversal and indexing
        bool openLoan;
        uint loanId;

        address borrower;
        address investor;
        uint interest_rate;
        uint duration;
        uint principal_amount;
        uint original_amount;
        uint amount_paid;
        uint startTime;
        uint appId;

    }

    // Methods
    function P2PLending(){
        // TODO Constructor may be added later
        numLoans = 1;
        numApplications = 1;
    }

    function createInvestor(string name){
        Investor investor;
        investor.name = name;
        investor.investor_public_key = msg.sender;
        investor.EXISTS = true;
        require (borrowers[msg.sender].EXISTS != true);
        investors[msg.sender] = investor;
        // investorArray[investorArray.length] = investor.investor_public_key;
        hasOngoingInvestment[msg.sender] = false;
        balances[msg.sender] = 0; // Init balance

    }

    function createBorrower(string name){
        Borrower borrower;
        borrower.name = name;
        borrower.borrower_public_key = msg.sender;
        borrower.EXISTS = true;
        require (investors[msg.sender].EXISTS != true);
        borrowers[msg.sender] = borrower;
        // borrowerArray[borrowerArray.length] = borrower.borrower_public_key;
        hasOngoingLoan[msg.sender] = false;
        hasOngoingApplication[msg.sender] = false;
        balances[msg.sender] = 0; // Init balance
    }

    function viewBalance() public returns (uint){
        return balances[msg.sender];
    }

    function deposit(uint amount) {
        balances[msg.sender] += amount;
    }

    function withdraw(uint amount) returns (uint) {
        require(amount <= balances[msg.sender]);
        balances[msg.sender] -= amount;
        return amount;
    }

    function transfer(address giver, address taker, uint amount){
        require(balances[giver] >= amount);
        balances[giver] -= amount;
        balances[taker] += amount;
    }

    function createApplication(uint duration, uint interest_rate, uint credit_amount, string otherData){

        require(hasOngoingLoan[msg.sender] == false);
        require(hasOngoingApplication[msg.sender] == false);
        applications[numApplications] = LoanApplication(true, numApplications, msg.sender, duration, credit_amount, interest_rate, otherData);
        // app.duration = duration;
        // app.interest_rate = interest_rate;
        // app.credit_amount = credit_amount;
        // app.otherData = otherData;
        // app.applicationId = numApplications;
        // app.borrower = msg.sender;
        // app.openApp = true;

        // current_applications[msg.sender] = app;
        numApplications += 1;
        hasOngoingApplication[msg.sender] = true;
    }

    function grantLoan(uint appId){
        //Check sufficient balance
        require(balances[msg.sender] >= applications[appId].credit_amount);
        require(hasOngoingInvestment[msg.sender] == false);

        // Take from sender and give to reciever
        balances[msg.sender] -= applications[appId].credit_amount;
        balances[applications[appId].borrower] += applications[appId].credit_amount;

        // Populate loan object
        loans[numLoans] = Loan(true, numLoans, applications[appId].borrower, msg.sender, applications[appId].interest_rate, applications[appId].duration, applications[appId].credit_amount, applications[appId].credit_amount, 0, now, appId);
        numLoans += 1;

        applications[appId].openApp = false;
        hasOngoingLoan[applications[appId].borrower] = true;
        hasOngoingInvestment[msg.sender] = true;


    }

    function repayLoan(uint amount){


        require(balances[msg.sender] >= amount);
        uint id_ = 0;
        for(uint i=1; i<=numLoans; i++)
        {
                if(loans[i].borrower == msg.sender)
                {
                    id_ = i;
                    break;
                }
        }
        Loan loan = loans[id_];
        require(loan.openLoan == true);

        uint p = loan.principal_amount;
        uint r = loan.interest_rate;
        uint t = loan.duration;
        uint n = 12;

        //uint finalAmount = p * (1 + r/n)**(n*t);
        //uint interest = p * (1 + r/n)**(n*)   1/12 2/12 3/12 --- duration/12

        //bhaumik
        uint timeElapsedInMonths = (now - loan.startTime);//(3600*24*30);
        timeElapsedInMonths = 1;
        // //3600 seconds in an hour, 24 hours a day, 30 days a month
        uint interest = p*(r)*(timeElapsedInMonths);
        // Check if amount is greater than monthly installment
        require(interest <=  amount);

        // Update balances
        balances[msg.sender] -= amount;
        balances[loan.investor] += amount;

        // Add amount to total amount paid
        loan.amount_paid += amount;
        amount -= interest;

        require(loan.principal_amount >= amount);
        loan.principal_amount -= amount;

        if(loan.principal_amount == 0)
        {
            loans[id_].openLoan = false;
            hasOngoingLoan[msg.sender] = false;
            hasOngoingApplication[msg.sender] = false;
            hasOngoingApplication[loan.investor] = false;
        }
        //bhaumik
    }

    function ifApplicationOpen(uint index) returns (bool){
        if(applications[index].openApp==true) return true;
        else return false;
    }

    function ifLoanOpen(uint index) returns (bool){
        if(loans[index].openLoan==true) return true;
        else return false;
    }

    function getApplicationData(uint index) returns (uint[], string, address){
        string otherData = applications[index].otherData;
        uint[] memory numericalData = new uint[](4);
        numericalData[0] = index;
        numericalData[1] = applications[index].duration;
        numericalData[2] = applications[index].credit_amount;
        numericalData[3] = applications[index].interest_rate;

        address borrower = applications[index].borrower;
        return (numericalData, otherData, borrower);
        // numericalData format = [index, duration, amount, interestrate]
    }

    function getLoanData(uint index) returns (uint[], address, address){
        uint[] memory numericalData = new uint[](8);
        numericalData[0] = index;
        numericalData[1] = loans[index].interest_rate;
        numericalData[2] = loans[index].duration;
        numericalData[3] = loans[index].principal_amount;
        numericalData[4] = loans[index].original_amount;
        numericalData[5] = loans[index].amount_paid;
        numericalData[6] = loans[index].startTime;
        numericalData[7] = loans[index].appId;

        return (numericalData, loans[index].borrower, loans[index].investor);
        // numericalData format = [index, interestrate, duration, p_amnt, o_amnt, paid_amnt, starttime, app_index]
    }

    function getNumApplications() returns (uint) { return numApplications;}
    function getNumLoans() returns (uint) { return numLoans;}
}