#ifndef COMMITTEE_H
#define COMMITTEE_H

#include <QString>

class Committee
{
private:
    QString m_name;
    int m_id;
    int m_score;

public:
    Committee(const QString &name);

    QString getName() const;
    void setName(const QString &name);

    int getId() const;
    void setId(int id);

    int getScore() const;
    void setScore(int score);
};

#endif // COMMITTEE_H
