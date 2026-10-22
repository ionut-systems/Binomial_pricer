#include <iostream>
#include <iomanip>
#include <cmath>
#include <algorithm>

// ... (Garde tes structures et fonctions binomialPricer existantes) ...

int main(int argc, char* argv[]) {
    OptionParams option;

    // Valeurs par défaut si lancé sans arguments
    option.S = 100.0;
    option.K = 100.0;
    option.r = 0.05;
    option.sigma = 0.20;
    option.T = 1.0;
    option.N = 500;

    // Si Python envoie les arguments, on les récupère dynamiquement
    if (argc >= 7) {
        option.S = std::stod(argv[1]);
        option.K = std::stod(argv[2]);
        option.r = std::stod(argv[3]);
        option.sigma = std::stod(argv[4]);
        option.T = std::stod(argv[5]);
        option.N = std::stoi(argv[6]);
    }

    double callPrice = binomialPricer(option, true);
    double putPrice = binomialPricer(option, false);

    std::cout << std::fixed << std::setprecision(4);
    std::cout << "==========================================\n";
    std::cout << "   BINOMIAL OPTION PRICER (CRR Model) v1.0\n";
    std::cout << "==========================================\n\n";
    std::cout << "Parametres de l'option :\n";
    std::cout << " - Prix Spot (S) : " << option.S << " EUR\n";
    std::cout << " - Strike (K) : " << option.K << " EUR\n";
    std::cout << " - Taux sans risque (r) : " << option.r * 100.0 << " %\n";
    std::cout << " - Volatilite (sigma) : " << option.sigma * 100.0 << " %\n";
    std::cout << " - Maturite (T) : " << option.T << " an(s)\n";
    std::cout << " - Nombre d'etapes (N) : " << option.N << "\n";
    std::cout << "------------------------------------------\n";
    std::cout << "[RESULTATS]\n";
    std::cout << " - Prix du Call Europeen : " << callPrice << " EUR\n";
    std::cout << " - Prix du Put Europeen  : " << putPrice << " EUR\n";
    std::cout << "==========================================\n";

    return 0;
}