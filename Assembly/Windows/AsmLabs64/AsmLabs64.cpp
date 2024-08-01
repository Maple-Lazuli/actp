#include "validation.h"

/*******************************************************************************
	Usage: AsmLabs64 [<server ip> <server port> <name>]
	
	Check with the instructor: If a server has been setup to report
	function size information,	you must set the command line parameters,
	otherwise, no parameters are needed.

	NOTE: If you are connecting to the server, you *must* have ScoreBoard.dll
	in the same directory as the executable.
*******************************************************************************/

int main(int argc, char* argv[])
{
	InitValidation(argc, argv);

	lab0_1();

	

	validate_lab1_1();
	validate_lab1_2();
	validate_lab1_3();
	validate_lab2_1();
	validate_lab2_2();
	validate_lab2_3();
	validate_lab2_4(); //BONUS
/*	MOVE THIS COMMENT TO ENABLE FUTURE LABS
	validate_lab3_1();
	validate_lab3_2();
	validate_lab3_3();
	validate_lab3_4();
	validate_lab3_5(); //SINGLE OR DOUBLE BONUS (will print if achieved)

	validate_lab4_1();
	validate_lab4_2();
	validate_lab4_3();
	validate_lab4_4();
	validate_lab4_5(); //BONUS

	validate_lab5_1();
	validate_lab5_2();
	validate_lab5_3(); // Bonus

	validate_lab6_1();
	validate_lab6_2();

	validate_lab6_3();
	validate_lab6_4(); //BONUS
	validate_lab6_5();

	validate_lab7_1();
	validate_lab7_2();
	validate_lab7_3(); //BONUS
	//lab7_4();// BONUS: manully validated

    validate_lab8_1();
	validate_lab8_2();
	validate_lab8_3();
	validate_lab8_4();
	validate_lab8_5();
	validate_lab8_6(); //BONUS

	validate_lab9_1();
	validate_lab9_2();

	validate_lab10_1();
	validate_lab10_2();

	//// Challenge labs
	validate_lab11_1();
	validate_lab11_2();
	validate_lab11_3();

	//// Additional challenges
	validate_lab11_4();
	validate_lab11_5();
	validate_lab11_6();
	validate_lab11_7();
	*/

	CloseValidation();
	printf( "------------------------\n"
			"Validation complete!\n");
	system("pause");

	return 0;
}

