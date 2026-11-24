#ifndef COMMITTEE_H
#define COMMITTEE_H

#include <QString>

class Committee
{
    friend class GA_manager;

public:
    Committee(const QString &name);

    QString getName() const;
    void setName(const QString &name);

    int getId() const;
    int getScore() const;

private:
    QString m_name;
    int m_id;
    int m_score;

    void setId(int id);
    void setScore(int score);
};

#endif // COMMITTEE_H
