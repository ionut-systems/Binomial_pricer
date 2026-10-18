#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iomanip>

struct OptionParams {
    double S;      // Prix actuel de l'actif sous-jacent (ex: 100.0)
    double K;      // Prix d'exercice / Strike (ex: 100.0)
    double r;      // Taux d'intérêt sans risque (ex: 0.05 pour 5%)
    double sigma;  // Volatilité (ex: 0.20 pour 20%)
    double T;      // Maturité en années (ex: 1.0 an)
    int N;         // Nombre d'étapes dans l'arbre (ex: 100)
};

double binomialPricer(const OptionParams& params, bool isCall = true) {
    double dt = params.T / params.N;
    double u = std::exp(params.sigma * std::sqrt(dt));
    double d = 1.0 / u;
    double p = (std::exp(params.r * dt) - d) / (u - d);
    double discount = std::exp(-params.r * dt);

    // Vecteur pour stocker les prix de l'option à la dernière étape (N)
    std::vector<double> prices(params.N + 1);
    for (int i = 0; i <= params.N; ++i) {
        // Calcul du prix de l'actif au nœud i à la maturité
        double spot_at_maturity = params.S * std::pow(u, params.N - i) * std::pow(d, i);
        
        if (isCall) {
            prices[i] = std::max(0.0, spot_at_maturity - params.K);
        } else {
            prices[i] = std::max(0.0, params.K - spot_at_maturity);
        }
    }

    // Remontée de l'arbre (Backward Induction)
    for (int step = params.N - 1; step >= 0; --step) {
        for (int i = 0; i <= step; ++i) {
            // Formule de valorisation espérée actualisée
            prices[i] = discount * (p * prices[i] + (1.0 - p) * prices[i + 1]);
        }
    }

    return prices[0]; // La valeur de l'option au sommet de l'arbre (aujourd'hui)
}

int main() {
    std::cout << "===========================================\n";
    std::cout << "   BINOMIAL OPTION PRICER (CRR Model) v1.0 \n";
    std::cout << "===========================================\n\n";

    OptionParams option;
    option.S = 100.0;  // Prix spot
    option.K = 100.0;  // Strike
    option.r = 0.05;   // Taux 5%
    option.sigma = 0.2;// Volatilité 20%
    option.T = 1.0;    // 1 an
    option.N = 500;    // 500 étapes

    double callPrice = binomialPricer(option, true);
    double putPrice = binomialPricer(option, false);

    std::cout << std::fixed << std::setprecision(4);
    std::cout << "Parametres de l'option :\n";
    std::cout << " - Prix Spot (S) : " << option.S << " EUR\n";
    std::cout << " - Strike (K)    : " << option.K << " EUR\n";
    std::cout << " - Taux sans risque (r) : " << (option.r * 100.0) << " %\n";
    std::cout << " - Volatilite (sigma)   : " << (option.sigma * 100.0) << " %\n";
    std::cout << " - Maturite (T)         : " << option.T << " an(s)\n";
    std::cout << " - Nombre d'etapes (N)  : " << option.N << "\n";
    std::cout << "-------------------------------------------\n";
    std::cout << "[RESULTATS]\n";
    std::cout << " Prix du Call Europeen : " << callPrice << " EUR\n";
    std::cout << " Prix du Put Europeen  : " << putPrice << " EUR\n";
    std::cout << "===========================================\n";

    std::cout << "\nAppuyez sur Entrée pour quitter...";
    std::cin.get();

    return 0;
}